defmodule Mix.Tasks.Pyairwaves.UpdateAircraftsOwner do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger

  NimbleCSV.define(MyParserOwner, separator: "\t", escape: "½")

  @moduledoc """
  Update the list of aircrafts Owners

  Cron recommanded: run one time per month
  """

  @shortdoc "Update the list of Aircraft Owners"
  def run(_) do
    # start the required apps & repos
    start_apps()

    Logger.info("Starting Aircrafts Owners update. (online)")
    HTTPoison.start()

    url = "http://data.flightairmap.com/data/owners.tsv.gz"

    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftOwner)
    Logger.info("Table cleaned.")

    Pyairwaves.Repo.transaction(
      fn ->
        HTTPoison.get!(url, [], []).body
        |> :zlib.gunzip()
        |> MyParserOwner.parse_string(skip_headers: true)
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
