defmodule Mix.Tasks.Pyairwaves.UpdateTranslations do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger

  NimbleCSV.define(MyParser, separator: "\t", escape: "\"")

  @moduledoc """
  Update the list of operators translations

  Cron recommanded: run one time per month
  """

  @shortdoc "Update the list of operators translations"
  def run(_) do
    # start the required apps & repos
    start_apps()

    Logger.info("Starting translations update. (Online)")
    HTTPoison.start()

    url = "http://data.flightairmap.com/data/translation.tsv.gz"

    Pyairwaves.Repo.delete_all(Pyairwaves.Translation)
    Logger.info("Table cleaned.")

    # CSV header:
    # reg, reg_correct, operator, operator_correct

    HTTPoison.get!(url, [], []).body
    |> :zlib.gunzip()
    |> MyParser.parse_string(skip_headers: true)
    |> Enum.map(fn [reg, reg_correct, operator, operator_correct] ->
      %{
        reg: reg,
        reg_correct: reg_correct,
        operator: operator,
        operator_correct: operator_correct,
        source: "translation.csv",
        inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
        updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second)
      }
    end)
    |> Enum.chunk_every(1000)
    |> Enum.map(fn chunk ->
      Pyairwaves.Repo.insert_all(Pyairwaves.Translation, chunk, on_conflict: :nothing)
    end)

    Logger.info("Update finished.")
  end
end
