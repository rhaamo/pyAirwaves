defmodule Pyairwaves.Aircraft do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "aircraft" do
    field :aircraft_description, :string, default: nil, size: 255
    field :aircraft_shadow, :string, default: nil, size: 255
    field :engine_count, :integer, default: nil
    field :engine_type, :string, default: nil
    field :icao, :string, size: 10
    field :manufacturer, :string, size: 255
    field :mfr, :string, default: nil
    field :official_page, :string, size: 255
    field :type, :string, size: 255
    field :wake_category, :string, size: 10
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [:icao, :type, :manufacturer, :official_page, :aircraft_shadow, :aircraft_description, :engine_type, :engine_count, :wake_category, :mfr])
    |> validate_required([:icao, :type, :manufacturer, :official_page])
    |> unique_constraint(:icao)
  end
end
