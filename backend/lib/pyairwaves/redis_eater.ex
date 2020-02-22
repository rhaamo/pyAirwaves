defmodule Pyairwaves.RedisEater do
  use GenServer
  require Logger

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
    Logger.debug("The pub/sub listener is subscribed to the #{inspect(channel)} channel")
    {:noreply, state}
  end

  # Handle incoming messages and dispatch then through our internal PubSub channel
  def handle_info(
        {:redix_pubsub, _pubsub, _ref, :message, %{channel: _channel, payload: message}},
        state
      ) do
    Phoenix.PubSub.broadcast(Pyairwaves.PubSub, "room:vehicles", {:redis_eat, message})
    # Logger.debug("Received from redis: #{inspect(message)}")
    {:noreply, state}
  end
end
