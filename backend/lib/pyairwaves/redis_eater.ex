defmodule Pyairwaves.RedisEater do
  use GenServer

  def start_link(_) do
    GenServer.start_link(__MODULE__, [])
  end

  def init(_) do
    settings = Application.get_env(:pyairwaves, :redis)
    {:ok, pubsub} = Redix.PubSub.start_link(settings)
    Redix.PubSub.subscribe(pubsub, "room:vehicles", self())
    {:ok, pubsub}
  end

  # pubsub listener subscribed to the channel
  def handle_info({:redix_pubsub, _pubsub, _ref, :subscribed, %{channel: channel}}, state) do
    IO.puts("The pub/sub listener is subscribed to the #{inspect(channel)} channel")
    {:noreply, state}
  end

  # Handle incoming messages and dispatch then through our internal PubSub channel
  def handle_info({:redix_pubsub, _pubsub, _ref, :message, %{channel: _channel, payload: message}}, state) do
    Phoenix.PubSub.broadcast(Pyairwaves.PubSub, message, message)
    IO.puts("Received from redis: #{inspect(message)}")
    {:noreply, state}
  end
end
