defmodule Pyairwaves.RedisEater do
  use GenServer
  require Logger
  require Pyairwaves.Utils
  require Ecto.Query

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
            {:redis_eat, archive_and_enhance_message(msg)}
          )
        end

      {:error, reason} ->
        Logger.error("Cannot decode incoming struct: #{reason}")
    end

    {:noreply, state, :hibernate}
  end

  defp compute_source_coverage(source, msg) do
    # Drop if position mode is 0 (none) or if the message doesn't have lat/lon
    if msg["srcPosMode"] == 0 or msg["srcPosMode"] == "0" or not Map.has_key?(msg, "lat") or
         not Map.has_key?(msg, "lon") do
      :ignored
    else
      # Logger.debug("Computing for source #{source.id}, #{source.name}, #{source.type}")
      distance =
        round(Geocalc.distance_between([msg["srcLat"], msg["srcLon"]], [msg["lat"], msg["lon"]]))

      bearing =
        Geocalc.bearing([msg["srcLat"], msg["srcLon"]], [msg["lat"], msg["lon"]])
        |> Pyairwaves.Utils.bearing_to_degrees()

      # Logger.info("Vehicle is #{distance} meters away from source on bearing #{bearing}")
      coverage = %{
        lat: msg["srcLat"],
        lon: msg["srcLon"],
        bearing: bearing,
        distance: distance
      }

      # IO.inspect(coverage)
      # IO.inspect(msg)

      Pyairwaves.States.SourceCoverage.add(source.id, coverage)
      # IO.inspect(Pyairwaves.States.SourceCoverage.find(source.id))
      :ok
    end
  end

  defp get_or_create_archive_source(msg) do
    %Pyairwaves.ArchiveSource{
      name: msg["srcName"],
      entrypoint: msg["entryPoint"],
      data_origin: msg["dataOrigin"],
      position_mode: msg["srcPosMode"],
      type: msg["type"]
    }
    |> Pyairwaves.Utils.put_if(:geom, Pyairwaves.Utils.to_geo_point(msg["srcLon"], msg["srcLat"]))
    |> Pyairwaves.Repo.insert(
      returning: true,
      on_conflict: {:replace, [:geom, :position_mode]},
      conflict_target: [:name, :type],
      log: false
    )
  end

  defp archive_and_enhance_message(%{"type" => "airAIS"} = msg) do
    # 1/ Fetch or create the ArchiveSource
    # TODO FIXME handle :error
    {:ok, source} = get_or_create_archive_source(msg)
    compute_source_coverage(source, msg)

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
    # TODO FIXME handle :error
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
    # TODO FIXME handle :error
    |> Pyairwaves.Repo.insert!(log: false)

    # Return the initial struct
    # TODO add missing callsign, dim_*, ship type, etc. if missing
    msg
  end

  # Two different methods for SBS and RAW Mode-S
  # Mode-S has more useful infos that SBS doesn't
  # But we still handle both to not have much feeder requirements

  # Handle and save a packet from SBS format
  defp archive_and_enhance_message(%{"type" => "airADSB", "srcAdsb" => "SBS"} = msg) do
    # 1/ Fetch or create the ArchiveSource
    # TODO FIXME handle :error
    {:ok, source} = get_or_create_archive_source(msg)
    compute_source_coverage(source, msg)

    # 2/ Fetch the aircraft and update if necessary
    aircraft =
      Pyairwaves.Repo.get_by(Pyairwaves.ArchiveAircraft, [hex_ident: msg["hexIdent"]], log: false)

    aircraft =
      if is_nil(aircraft) do
        # Create one because it does not exists
        %Pyairwaves.ArchiveAircraft{
          hex_ident: msg["hexIdent"],
          inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second)
        }
      else
        # Aircraft exists, return it
        aircraft
      end

    # Build a changeset
    Pyairwaves.ArchiveAircraft.changeset(aircraft, %{})
    # Save it
    # TODO FIXME handle :error
    |> Pyairwaves.Repo.insert_or_update!(log: false)

    # No microseconds from the struct
    generated =
      msg["generated"]
      # TODO FIXME handle :error
      |> Timex.parse!("%Y-%m-%d %H:%M:%S", :strftime)
      |> NaiveDateTime.truncate(:second)

    # 3/ Archive the rest of the message
    %Pyairwaves.ArchiveAircraftMessage{
      source_type: "SBS",
      hex_ident: msg["hexIdent"],
      msg_type: msg["msgType"],
      transmission_type: msg["transmissionType"],
      session_id: msg["sessionId"],
      aircraft_id: msg["aircraftId"],
      flight_id: msg["flightId"],
      generated: generated,
      callsign: msg["callsign"],
      altitude: msg["altitude"],
      ground_speed: msg["ground_speed"],
      track: msg["track"],
      geom: Pyairwaves.Utils.to_geo_point(msg["lon"], msg["lat"]),
      vertical_rate: msg["vertical_rate"],
      squawk: msg["squawk"],
      alert: msg["alert"],
      emergency: msg["emergency"],
      spi_ident: msg["spi_ident"],
      is_on_ground: msg["is_on_ground"],
      # "logged"
      inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
      archive_aircraft_id: aircraft.id,
      archive_source_id: source.id
    }
    # TODO FIXME handle :error
    |> Pyairwaves.Repo.insert!(log: false)

    # 4/ Add additionnal stuff to the msg
    q_extras =
      Ecto.Query.from(am in Pyairwaves.AircraftMode,
        left_join: a in Pyairwaves.Aircraft,
        on: am.icao_type_code == a.icao,
        where: am.mode_s == ^msg["hexIdent"],
        select: %{mode_s_country: am.mode_s_country, description: a.aircraft_description},
        limit: 1
      )

    extras = Pyairwaves.Repo.one(q_extras, log: false) || %{mode_s_country: nil, description: nil}

    # 5/ Return it
    msg
    # In dump1090 this is aircraft heading, consider it for all
    |> Map.put("heading", msg["track"])
    # renamed but not in front yet and ais
    |> Map.put("alt", msg["altitude"])
    # same
    |> Map.put("addr", msg["hexIdent"])
    # Extras
    |> Pyairwaves.Utils.put_if("icaoAACC", extras.mode_s_country)
    |> Pyairwaves.Utils.put_if("category", extras.description)
  end

  # Handle and save a packet from RAW Mode-S format
  defp archive_and_enhance_message(%{"type" => "airADSB", "srcAdsb" => "RAW MODE-S"} = msg) do
    # 1/ Fetch or create the ArchiveSource
    {:ok, source} = get_or_create_archive_source(msg)
    compute_source_coverage(source, msg)

    # 2/ Fetch the aircraft and update if necessary
    # 3/ Archive the rest of the message
    # 4/ Add additionnal stuff to the msg
    # 5/ Return it
    msg
    # renamed but not in front yet and ais
    |> Map.put("alt", msg["altitude"])
    # same
    |> Map.put("addr", msg["hexIdent"])
  end
end
