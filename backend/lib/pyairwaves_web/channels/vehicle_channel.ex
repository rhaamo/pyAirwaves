defmodule PyairwavesWeb.VehicleChannel do
  use Phoenix.Channel
  require Logger

  @moduledoc """
  PubSub channel "room:vehicles"
  """

  def join("room:vehicles", _message, socket) do
    {:ok, socket}
  end

  # Broadcast through the internal PubSub to websocket from redis PubSub
  def handle_info({:redis_eat, message}, socket) do
    push(socket, "new_msg", %{
      data: Pyairwaves.MessageProcessor.archive_and_enhance_redis_message(message)
    })

    {:noreply, socket}
  end

  def handle_info({:ais_client, message}, socket) do
    Logger.warn("FIXME FIXME")
    push(socket, "new_msg", %{data: message})
    {:noreply, socket}
  end
end
