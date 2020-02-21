defmodule Mix.Tasks.Pyairwaves.UpdateAircraftsModeS do
  use Mix.Task

  require Logger

  @moduledoc """
  Update the list of aircrafts Mode S

  Cron recommanded: run one time per month
  """

  defp parse_aircraft_mode(row) do
    type_flight = case row[:UserString4] do
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
      is_private: private  # might be useful one day
    }
  end


  @shortdoc "Update the list of Aircraft Mode S"
  def run(_) do
    Application.ensure_all_started(:pyairwaves)
    Temp.track!

    Logger.info("Starting Aircrafts ModeS update. (Online)")
    HTTPoison.start()

    url = "http://data.flightairmap.com/data/BaseStation.sqb.gz"

    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftMode)
    Logger.info("Table cleaned.")

    temp_file = Temp.path!

    datas = HTTPoison.get!(url, [], []).body
    |> :zlib.gunzip()
    File.write!(temp_file, datas)

    Logger.info("File downloaded.")

    Pyairwaves.Repo.transaction(fn ->
      # It uses SQlite3...
      Sqlitex.with_db(temp_file, fn (db) ->
        Sqlitex.query(db, "SELECT LastModified, ModeS, ModeSCountry, Registration, ICAOTypeCode, UserString4, RegisteredOwners, Registration from Aircraft")
      end)
      |> elem(1)
      |> Enum.map(fn (row) ->
        Pyairwaves.Repo.insert!(parse_aircraft_mode(row), log: false)
        case row[:RegisteredOwners] do
          "" -> nil
          nil -> nil
          "private" -> Pyairwaves.Repo.insert!(parse_owner(row, true), log: false)
          _ -> Pyairwaves.Repo.insert!(parse_owner(row, false), log: false)
        end
      end)
    end, timeout: :infinity, log: false)

    Temp.cleanup
    Logger.info("Update finished.")
  end
end
