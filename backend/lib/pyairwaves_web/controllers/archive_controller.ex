defmodule PyairwavesWeb.ArchiveController do
  use PyairwavesWeb, :controller
  require Ecto.Query

  def ais_quick(conn, _params) do
    sources =
      Pyairwaves.ArchiveSource
      |> Ecto.Query.order_by([a], asc: a.inserted_at)
      |> Pyairwaves.Repo.all()

    ships =
      Pyairwaves.ArchiveShip
      |> Ecto.Query.order_by([a], asc: a.inserted_at)
      |> Ecto.Query.limit(15)
      |> Pyairwaves.Repo.all()

    render(conn, "ais_quick.html",
      version: Pyairwaves.Application.version(),
      page: "ais_quick",
      sources: sources,
      ships: ships,
      count_sources: Enum.count(sources),
      count_ships: Pyairwaves.Repo.one(Ecto.Query.from a in "archive_ship", select: count(a.id)),
      count_messages: Pyairwaves.Repo.one(Ecto.Query.from a in "archive_ship_message", select: count(a.id))
    )
  end
end
