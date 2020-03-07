defmodule Pyairwaves.AisClient do
  use GenServer
  require Logger

  def start_link(_) do
    {:ok, ais} = AIS.new()
    GenServer.start_link(__MODULE__, %{socket: nil, ais: ais}, name: __MODULE__)
  end

  def init(state) do
    send(self(), :connect)
    {:ok, state}
  end

  def handle_info(:connect, state) do
    settings = Application.get_env(:pyairwaves, :ais_client)
    Logger.info("AIS Client connecting to #{settings[:host]}:#{settings[:port]}")
    case :gen_tcp.connect(settings[:host], settings[:port], [:binary, active: true]) do
      {:ok, socket} ->
        Logger.info("AIS Client connected to #{settings[:host]}:#{settings[:port]}")
        {:noreply, %{state | socket: socket}}
      {:error, reason} ->
        disconnect(state, reason)
    end
  end

  def handle_info({:tcp, _, data}, state) do
    data = data
    |> String.trim
    Logger.info("Received '#{data}'")
    case AIS.parse(state[:ais], data) do
      {:ok, decoded} ->
        Logger.debug("Got a full packet:")
        IO.inspect(decoded)
      {:incomplete, decoded} ->
        Logger.debug("Incomplete one:")
        IO.inspect(decoded)
    end
    {:noreply, state}
  end

  def handle_info({:tcp_closed, _}, state) do
    {:stop, :normal, state}
  end

  def handle_info({:tcp_error, _}, state) do
    {:stop, :normal, state}
  end

  def disconnect(state, reason) do
    Logger.info("AIS Client disconnected: #{reason}")
    {:stop, :normal, state}
  end
end
