defmodule Pyairwaves.AisClient do
  use GenServer, restart: :transient
  require Logger

  def start_link({cfg}) do
    {:ok, ais} = AIS.new()
    log_name = "#{cfg[:name]} #{cfg[:host]}"
    GenServer.start_link(__MODULE__, %{socket: nil, ais: ais, cfg: cfg, log_name: log_name})
  end

  def init(state) do
    send(self(), :connect)
    {:ok, state}
  end

  def handle_info(:connect, state) do
    settings = state[:cfg]

    Logger.info(
      "[#{state[:log_name]}] AIS Client connecting to #{settings[:host]}:#{settings[:port]}"
    )

    case :gen_tcp.connect(settings[:host], settings[:port], [:binary, active: true]) do
      {:ok, socket} ->
        Logger.info(
          "[#{state[:log_name]}] AIS Client connected to #{settings[:host]}:#{settings[:port]}"
        )

        {:noreply, %{state | socket: socket}}

      {:error, reason} ->
        disconnect(state, reason)
    end
  end

  def handle_info({:tcp, _, data}, state) do
    data
    |> String.trim()
    |> String.split()
    |> Enum.each(fn d ->
      case AIS.parse(state[:ais], d) do
        {:ok, _decoded} ->
          nil

        # Logger.debug("full: #{d}")
        {:error, {:invalid_checksum, _decoded}} ->
          Logger.error("[#{state[:log_name]}] checksum: #{d}")

        {:error, {:incomplete, _}} ->
          nil

        {:error, {:invalid, _}} ->
          Logger.error("[#{state[:log_name]}] invalid: #{d}")
      end
    end)

    {:noreply, state}
  end

  def handle_info({:tcp_closed, _}, state) do
    {:stop, :normal, state}
  end

  def handle_info({:tcp_error, _}, state) do
    {:stop, :normal, state}
  end

  def disconnect(state, reason) do
    Logger.info("[#{state[:log_name]}] AIS Client disconnected: #{reason}")
    {:stop, :normal, state}
  end
end
