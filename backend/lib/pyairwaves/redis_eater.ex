defmodule Pyairwaves.RedisEater do
  use GenServer
  require Logger

  @moduledoc """
  Receives messages from the Redis PubSub, pass is through the MessageProcessor and forward them to the internal PubSub
  """

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
    case Jason.decode(message) do
      {:ok, msg} ->
        # TODO: Broadcast only if lat and lon are available
        if msg["lat"] >= 91.0 or msg["lat"] <= -91.0 or msg["lon"] >= 181.0 or
             msg["lon"] <= -181.0 do
          # bogus datas if anything not in -90/90 or -180/180
          {:noreply, state, :hibernate}
        else
          Phoenix.PubSub.broadcast(
            Pyairwaves.PubSub,
            "room:vehicles",
            {:redis_eat, Pyairwaves.MessageProcessor.archive_and_enhance_message(msg)}
          )
        end

      {:error, reason} ->
        Logger.error("Cannot decode incoming struct: #{reason}")
    end

    {:noreply, state, :hibernate}
  end
end
