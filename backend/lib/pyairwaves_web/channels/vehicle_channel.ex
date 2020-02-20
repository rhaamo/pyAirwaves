defmodule PyairwavesWeb.VehicleChannel do
  use Phoenix.Channel
  require Logger

  def join("room:vehicles", _message, socket) do
    {:ok, socket}
  end

end