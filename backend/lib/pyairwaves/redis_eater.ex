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

  def get_or_create_archive_source(msg) do
    %Pyairwaves.ArchiveSource{
      name: msg["srcName"],
      entrypoint: msg["entryPoint"],
      data_origin: msg["dataOrigin"],
      position_mode: msg["srcPosMode"],
      type: msg["type"]
    }
    |> Pyairwaves.Utils.put_if(:geom, Pyairwaves.Utils.to_geo_point(msg["lon"], msg["lat"]))
    |> Pyairwaves.Repo.insert!(on_conflict: :nothing, log: false)
  end

  defp archive_and_enhance_message(%{"type" => "airAIS"} = msg) do
    # 1/ Fetch or create the ArchiveSource
    source = get_or_create_archive_source(msg)

    # 2/ Fetch the ship and update if necessary
    ship = Pyairwaves.Repo.get_by(Pyairwaves.ArchiveShip, [mmsi: msg["mmsi"]], log: false)

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
    |> Pyairwaves.Repo.insert_or_update!(log: false)

    # 3/ Archive the rest of the message
    %Pyairwaves.ArchiveShipMessage{
      mmsi: msg["mmsi"],
      raw: msg["raw"],
      assembled: msg["isAssembled"],
      archive_ship_id: ship.id,
      archive_source_id: source.id
    }
    |> Pyairwaves.Utils.put_if(:geom, Pyairwaves.Utils.to_geo_point(msg["lon"], msg["lat"]))
    |> Pyairwaves.Utils.put_if(:position_accuracy, msg["posAcc"])
    |> Pyairwaves.Utils.put_if(:maneuver, msg["maneuver"])
    |> Pyairwaves.Utils.put_if(:raim, msg["raim"])
    |> Pyairwaves.Utils.put_if(:radio_status, msg["radioStatus"])
    |> Pyairwaves.Utils.put_if(:destination, msg["destination"])
    |> Pyairwaves.Utils.put_if(:callsign, msg["callsign"])
    |> Pyairwaves.Utils.put_if(:epfd, msg["epfdMeta"])
    |> Pyairwaves.Utils.put_if(:navigation_status, msg["navStatMeta"])
    |> Pyairwaves.Utils.put_if(:eta, msg["navStatMeta"])
    |> Pyairwaves.Utils.put_if(:heading, Pyairwaves.Utils.to_float(msg["heading"]))
    |> Pyairwaves.Utils.put_if(
      :course_over_ground,
      Pyairwaves.Utils.to_float(msg["courseOverGnd"])
    )
    |> Pyairwaves.Utils.put_if(:turn_rate, Pyairwaves.Utils.to_float(msg["turnRt"]))
    |> Pyairwaves.Utils.put_if(:draught, Pyairwaves.Utils.to_float(msg["draught"]))
    |> Pyairwaves.Repo.insert!(log: false)

    # Return the initial struct
    # TODO add missing callsign, dim_*, ship type, etc. if missing
    msg
  end

  # Two different methods for SBS and RAW Mode-S
  # Mode-S has more useful infos that SBS doesn't
  # But we still handle both to not have much feeder requirements

  @doc "Handle and save a packet from SBS format"
  defp archive_and_enhance_message(%{"type" => "airADSB", "srcAdsb" => "SBS"} = msg) do
    # 1/ Fetch or create the ArchiveSource
    _source = get_or_create_archive_source(msg)

    # 2/ Fetch the aircraft and update if necessary
    # 3/ Archive the rest of the message
    # 4/ Add additionnal stuff to the msg
    # 5/ Return it
    msg
  end

  @doc "Handle and save a packet from RAW Mode-S format"
  defp archive_and_enhance_message(%{"type" => "airADSB", "srcAdsb" => "RAW MODE-S"} = msg) do
    # 1/ Fetch or create the ArchiveSource
    _source = get_or_create_archive_source(msg)

    # 2/ Fetch the aircraft and update if necessary
    # 3/ Archive the rest of the message
    # 4/ Add additionnal stuff to the msg
    # 5/ Return it
    msg["heading"] = msg["track"] # In dump1090 this is aircraft heading, consider it for all
    msg["alt"] = msg["altitude"] # renamed but not in front yet and ais
    msg["addr"] = msg["hexIdent"] # same
    msg
  end
end
