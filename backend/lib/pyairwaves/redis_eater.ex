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
    message =
      Jason.decode!(message)
      |> archive_and_enhance_message

    Phoenix.PubSub.broadcast(Pyairwaves.PubSub, "room:vehicles", {:redis_eat, message})
    # Logger.debug("Received from redis: #{inspect(message)}")
    {:noreply, state, :hibernate}
  end

  defp archive_and_enhance_message(%{"type" => "airAIS"} = msg) do
    # 1/ Fetch the ship
    ship = Pyairwaves.Repo.get_by(Pyairwaves.ArchiveShip, mmsi: msg["mmsi"])

    ship =
      if is_nil(ship) do
        # Create one because it does not exists
        %Pyairwaves.ArchiveShip{
          mmsi: msg["mmsi"],
          mmsi_type: msg["mmsiType"],
          mmsi_cc: msg["mmsiCC"],
          inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second)
        }
      else
        # Ship exists, return it
        ship
      end

    # Then build the changeset of changing things
    changes =
      %{}
      |> Pyairwaves.Utils.put_if(:callsign, msg["callsign"])
      |> Pyairwaves.Utils.put_if(:dim_to_bow, msg["dimToBow"])
      |> Pyairwaves.Utils.put_if(:dim_to_stern, msg["dimToStern"])
      |> Pyairwaves.Utils.put_if(:dim_to_port, msg["dimToPort"])
      |> Pyairwaves.Utils.put_if(:dim_to_starboard, msg["dimToStarboard"])
      |> Pyairwaves.Utils.put_if(:ship_type, msg["shipTypeMeta"])

    # Update timestamp if anything changed
    changes =
      if Enum.count(changes) > 0 do
        Map.put(changes, :updated_at, NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second))
      else
        changes
      end

    # Build a changeset
    Pyairwaves.ArchiveShip.changeset(ship, changes)
    # Save it
    |> Pyairwaves.Repo.insert_or_update!()

    # Return the initial struct
    msg
  end

  defp archive_and_enhance_message(%{"type" => "airADSB"} = msg) do
    IO.puts("storing ADSB message...")
    msg
  end
end
