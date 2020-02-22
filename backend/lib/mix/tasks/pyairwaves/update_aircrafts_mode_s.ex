defmodule Mix.Tasks.Pyairwaves.UpdateAircraftsModeS do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger

  @moduledoc """
  Update the list of aircrafts Mode S and Aircraft Owners

  Cron recommanded: run one time per month
  """

  defp parse_aircraft_mode(row) do
    type_flight =
      case row[:UserString4] do
        "M" -> "military"
        _ -> nil
      end

    %Pyairwaves.AircraftMode{
      # updated_at: row[:LastModified],
      # inserted_at: row[:LastModified],
      updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
      inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
      mode_s: row[:ModeS],
      mode_s_country: row[:ModeSCountry],
      registration: row[:Registration],
      icao_type_code: row[:ICAOTypeCode],
      source: "BaseStation.sqb",
      type_flight: type_flight
    }
  end

  defp parse_owner(row, private) do
    %Pyairwaves.AircraftOwner{
      registration: row[:Registration],
      source: "BaseStation.sqb",
      owner: row[:RegisteredOwners],
      # might be useful one day
      is_private: private
    }
  end

  @shortdoc "Update the list of Aircraft Mode S and Aircraft Owners"
  def run(_) do
    # start the required apps & repos
    start_apps()

    Temp.track!()

    Logger.info("Starting Aircrafts ModeS update. (Online)")
    HTTPoison.start()

    url = "http://data.flightairmap.com/data/BaseStation.sqb.gz"

    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftMode)
    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftOwner)
    Logger.info("Table cleaned.")

    temp_file = Temp.path!()

    datas =
      HTTPoison.get!(url, [], []).body
      |> :zlib.gunzip()

    File.write!(temp_file, datas)

    Logger.info("File downloaded.")

    Pyairwaves.Repo.transaction(
      fn ->
        # It uses SQlite3...
        Sqlitex.with_db(temp_file, fn db ->
          Sqlitex.query(
            db,
            "SELECT LastModified, ModeS, ModeSCountry, Registration, ICAOTypeCode, UserString4, RegisteredOwners, Registration from Aircraft"
          )
        end)
        |> elem(1)
        |> Enum.map(fn row ->
          Pyairwaves.Repo.insert!(parse_aircraft_mode(row), log: false)

          is_private =
            case String.downcase(to_string(row[:RegisteredOwners])) do
              "" -> nil
              "private" -> true
              _ -> false
            end

          Pyairwaves.Repo.insert!(parse_owner(row, is_private), log: false)
        end)
      end,
      timeout: :infinity,
      log: false
    )

    # TODO cleanup from ACARS
    # q = db.session.query(AircraftModes.mode_s).filter(AircraftModes.source == "ACARS")
    # db.session.query(AircraftModes).filter(and_(AircraftModes.source == fname, AircraftModes.mode_s.in_(q))).delete(
    #     synchronize_session="fetch"
    # )

    Temp.cleanup()
    Logger.info("Update finished.")
  end
end
