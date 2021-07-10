defmodule Pyairwaves.AisClientsSupervisor do
  use DynamicSupervisor
  require Logger

  @moduledoc """
  Supervise the starting of one AisClient per item in config
  """

  def start_link(_) do
    DynamicSupervisor.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def init(:ok) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end

  def start_ais_clients do
    ais_clients_config = Application.get_env(:pyairwaves, :ais_clients)

    Enum.each(ais_clients_config, fn x ->
      add_ais_client(x)
    end)
  end

  def add_ais_client(cfg) do
    Logger.info("Starting one AisClient for: #{cfg[:name]}")
    child_spec = {Pyairwaves.AisClient, {cfg}}
    # child_spec = Pyairwaves.AisClient.child_spec({cfg})
    DynamicSupervisor.start_child(__MODULE__, child_spec)
  end

  def remove_ais_client(ais_client_pid) do
    DynamicSupervisor.terminate_child(__MODULE__, ais_client_pid)
  end

  def children do
    DynamicSupervisor.which_children(__MODULE__)
  end

  def count_children do
    DynamicSupervisor.count_children(__MODULE__)
  end
end
