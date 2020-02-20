defmodule PyairwavesWeb.MapController do
  use PyairwavesWeb, :controller

  def map(conn, _params) do
    render(conn, "map.html")
  end
end
