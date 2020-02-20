defmodule PyairwavesWeb.MapController do
  use PyairwavesWeb, :controller

  def map(conn, _params) do
    render(conn, "map.html", version: Pyairwaves.Application.version(), page: "map")
  end
end
