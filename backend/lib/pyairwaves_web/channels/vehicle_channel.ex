defmodule PyairwavesWeb.VehicleChannel do
  use Phoenix.Channel

  require Logger

  def join("room:vehicles", _message, socket) do
    {:ok, socket}
  end

  # Broadcast through the internal PubSub to websocket from redis PubSub
  def handle_info({:redis_eat, message}, socket) do
    push(socket, "new_msg", %{data: message})
    {:noreply, socket}
  end
end
