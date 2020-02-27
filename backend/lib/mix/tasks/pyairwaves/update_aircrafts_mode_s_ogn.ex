defmodule Mix.Tasks.Pyairwaves.UpdateAircraftsModeSogn do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger
  require Ecto.Query

  NimbleCSV.define(UAMSOGNParser, separator: ",", escape: "'")

  @moduledoc """
  Update the list of aircrafts Mode S from Open Glider Network

  Cron recommanded: run one time per month
  """

  defp parse_aircraft_mode(row) do
    [_device_type, device_id, aircraft_model, registration, _cn, _tracked, _identified] = row

    # Try to determine ICAO, default is GLID (not handled)
    [an0, an1] =
      case String.split(aircraft_model, " ") do
        [a, b | _] -> [a, b]
        [a] -> [a, ""]
      end

    query =
      if String.length(an0) > 1 and String.length(an1) > 3 do
        Pyairwaves.Aircraft
        |> Ecto.Query.where([a], a.type == ^"%#{aircraft_model}%" and a.type == ^"%#{an0}%")
      else
        Pyairwaves.Aircraft
        |> Ecto.Query.where([a], like(a.type, ^"%#{aircraft_model}%"))
      end

    aircraft =
      query
      |> Ecto.Query.select([a], a.icao)
      |> Ecto.Query.first()
      |> Pyairwaves.Repo.one(log: false)

    icao_type_code = aircraft || ""

    am = %Pyairwaves.AircraftMode{
      mode_s: device_id,
      registration: registration,
      updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
      inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
      source: "ogn.csv",
      icao_type_code: icao_type_code
    }

    if registration != "" or registration != "0000" or icao_type_code != "" do
      {:ok, am}
    else
      {:ignored, nil}
    end
  end

  @shortdoc "Update the list of aircrafts Mode S from Open Glider Network"
  def run(_) do
    # start the required apps & repos
    start_apps()

    Logger.info("Starting Aircrafts ModeS from Open Glider Network update. (Online)")
    Logger.info("This can take some time.")
    HTTPoison.start()

    url = "http://ddb.glidernet.org/download/"

    # Delete matching source == "ogn.csv" or source is none or source == ""
    Pyairwaves.AircraftMode
    |> Ecto.Query.where([am], am.source == "ogn.csv" or is_nil(am.source) or am.source == "")
    |> Pyairwaves.Repo.delete_all()

    Logger.info("Table cleaned.")

    Pyairwaves.Repo.transaction(
      fn ->
        # CSV Header:
        # DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED
        HTTPoison.get!(url, [], []).body
        |> UAMSOGNParser.parse_string(skip_headers: true)
        |> Enum.map(fn row ->
          {:ok, am} = parse_aircraft_mode(row)
          Pyairwaves.Repo.insert!(am, log: false)
        end)
      end,
      log: false,
      timeout: :infinity
    )

    # TODO cleanup from ACARS
    # q = db.session.query(AircraftModes.mode_s).filter(AircraftModes.source == "ACARS")
    # db.session.query(AircraftModes).filter(and_(AircraftModes.source == fname, AircraftModes.mode_s.in_(q))).delete(
    #     synchronize_session="fetch"
    # )

    Logger.info("Update finished.")
  end
end
