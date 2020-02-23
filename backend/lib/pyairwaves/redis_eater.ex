defmodule Pyairwaves.RedisEater do
  use GenServer
  require Logger
  require Pyairwaves.Utils

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
    decoded_message = Jason.decode!(message)
    Phoenix.PubSub.broadcast(Pyairwaves.PubSub, "room:vehicles", {:redis_eat, decoded_message})
    # Logger.debug("Received from redis: #{inspect(message)}")
    archive_message(decoded_message)
    {:noreply, state, :hibernate}
  end

  defp archive_message(%{"type" => "airAIS"} = msg) do
    # 1/ Store the ship itself
    ship = %Pyairwaves.ArchiveShip{
      mmsi: msg["mmsi"],
      mmsi_type: msg["mmsiType"],
      mmsi_cc: msg["mmsiCC"],
      inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
      updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second)
    }
    |> Pyairwaves.Utils.put_if(:callsign, msg["callsign"])
    |> Pyairwaves.Utils.put_if(:dim_to_bow, msg["dim_to_bow"])
    |> Pyairwaves.Utils.put_if(:dim_to_stern, msg["dim_to_stern"])
    |> Pyairwaves.Utils.put_if(:dim_to_port, msg["dim_to_port"])
    |> Pyairwaves.Utils.put_if(:dim_to_starboard, msg["dim_to_starboard"])
    |> Pyairwaves.Utils.put_if(:shipType, msg["shipType"])

    Pyairwaves.Repo.insert!(ship,
      on_conflict:
        {:replace,
         [
           :mmsi_cc,
           :callsign,
           :dim_to_bow,
           :dim_to_stern,
           :dim_to_port,
           :dim_to_starboard,
           :ship_type,
           :updated_at
         ]},
         conflict_target: [:mmsi]
    )

    # 2/ Then the message
  end

  defp archive_message(%{"type" => "airADSB"} = _message) do
    IO.puts("storing ADSB message...")
  end
end
