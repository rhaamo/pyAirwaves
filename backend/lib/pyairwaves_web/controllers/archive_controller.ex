defmodule PyairwavesWeb.ArchiveController do
  use PyairwavesWeb, :controller
  require Ecto.Query

  def sources_coverage(conn, _params) do
    sources =
      Pyairwaves.ArchiveSource
      |> Ecto.Query.order_by([a], asc: a.inserted_at)
      |> Pyairwaves.Repo.all()
      |> Enum.chunk_every(4)

    render(conn, "sources_coverage.html",
      version: Pyairwaves.Application.version(),
      page: "sources_coverage",
      sources: sources
    )
  end

  def ais_quick(conn, _params) do
    sources =
      Pyairwaves.ArchiveSource
      |> Ecto.Query.where(type: "airAIS")
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
      count_ships: Pyairwaves.Repo.one(Ecto.Query.from(a in "archive_ship", select: count(a.id))),
      count_messages:
        Pyairwaves.Repo.one(Ecto.Query.from(a in "archive_ship_message", select: count(a.id)))
    )
  end

  def adsb_quick(conn, _params) do
    sources =
      Pyairwaves.ArchiveSource
      |> Ecto.Query.where(type: "airADSB")
      |> Ecto.Query.order_by([a], asc: a.inserted_at)
      |> Pyairwaves.Repo.all()

    q_aircrafts =
      Ecto.Query.from(aa in Pyairwaves.ArchiveAircraft,
        left_join: am in Pyairwaves.AircraftMode,
        on: am.mode_s == aa.hex_ident,
        left_join: a in Pyairwaves.Aircraft,
        on: am.icao_type_code == a.icao,
        select: %{
          mode_s: am.mode_s,
          mode_s_country: am.mode_s_country,
          description: a.aircraft_description,
          engine_count: a.engine_count,
          engine_type: a.engine_type,
          manufacturer: a.manufacturer,
          types: a.type,
          found: aa.inserted_at
        },
        limit: 15,
        order_by: [desc: aa.inserted_at]
      )

    aircrafts = Pyairwaves.Repo.all(q_aircrafts, timeout: :infinity)

    render(conn, "adsb_quick.html",
      version: Pyairwaves.Application.version(),
      page: "adsb_quick",
      sources: sources,
      aircrafts: aircrafts,
      count_sources: Enum.count(sources),
      count_aircrafts:
        Pyairwaves.Repo.one(Ecto.Query.from(a in Pyairwaves.ArchiveAircraft, select: count(a.id))),
      count_messages:
        Pyairwaves.Repo.one(
          Ecto.Query.from(a in Pyairwaves.ArchiveAircraftMessage, select: count(a.id))
        )
    )
  end
end
