defmodule PyairwavesWeb.AppController do
  use PyairwavesWeb, :controller

  def about(conn, _params) do
    render(conn, "about.html", version: Pyairwaves.Application.version(), page: "about")
  end
end
