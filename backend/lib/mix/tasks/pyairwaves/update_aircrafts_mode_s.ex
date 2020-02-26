defmodule Mix.Tasks.Pyairwaves.UpdateAircraftsModeS do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger

  NimbleCSV.define(MyParserModeS, separator: "\t", escape: "½")

  @moduledoc """
  Update the list of aircrafts Mode S and Owners

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

  @shortdoc "Update the list of Aircraft Owner"
  def run(_) do
    start_apps()

    Logger.info("Starting Aircrafts ModeS update. (online)")

    # start the required apps & repos
    HTTPoison.start()

    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftMode)
    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftOwner)
    Logger.info("Tables cleaned.")

    import_mode_s_from_fam()
    import_mode_s_from_basestation()
    import_owners_from_fam()
  end

  def import_mode_s_from_fam() do
    Logger.info("Importing from modes TSV")

    url = "http://data.flightairmap.com/data/modes.tsv.gz"

    Pyairwaves.Repo.transaction(
      fn ->
        HTTPoison.get!(url, [], []).body
        |> :zlib.gunzip()
        |> MyParserModeS.parse_string(skip_headers: true)
        |> Enum.map(fn [
                         _first_created,
                         _last_modified,
                         mode_s,
                         mode_s_country,
                         registration,
                         icao_type_code,
                         type_flight
                       ] ->
          %Pyairwaves.AircraftMode{
            updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
            inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
            mode_s: mode_s,
            mode_s_country: mode_s_country,
            registration: registration,
            icao_type_code: icao_type_code,
            type_flight: type_flight,
            source: "modes.tsv"
          }
        end)
        |> Enum.map(fn item ->
          Pyairwaves.Repo.insert!(item, on_conflict: :nothing, log: false)
        end)
      end,
      timeout: :infinity,
      log: false
    )

    Logger.info("TSV Import done.")
  end

  def import_mode_s_from_basestation() do
    Logger.info("Importing from modes BaseStation")

    Temp.track!()

    url = "http://data.flightairmap.com/data/BaseStation.sqb.gz"

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
    Logger.info("BaseStation Import done.")
  end

  def import_owners_from_fam() do
    Logger.info("Starting Aircrafts Owners update. (online)")

    url = "http://data.flightairmap.com/data/owners.tsv.gz"

    Pyairwaves.Repo.transaction(
      fn ->
        HTTPoison.get!(url, [], []).body
        |> :zlib.gunzip()
        |> MyParserModeS.parse_string(skip_headers: true)
        |> Enum.map(fn [
                         registration,
                         base,
                         owner,
                         _date_first_reg
                       ] ->
          %Pyairwaves.AircraftOwner{
            base: base,
            # not contained in file
            date_first_reg: nil,
            # unknown
            is_private: false,
            owner: owner,
            registration: registration,
            source: "owners.tsv"
          }
        end)
        |> Enum.map(fn item ->
          Pyairwaves.Repo.insert!(item, on_conflict: :nothing, log: false)
        end)
      end,
      timeout: :infinity,
      log: false
    )

    Logger.info("Owners imported.")
  end
end
