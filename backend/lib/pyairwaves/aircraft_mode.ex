defmodule Pyairwaves.AircraftMode do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  # Indexes on: mode_s, mode_s_country, registration and icao_type_code

  schema "aircraft_mode" do
    field :icao_type_code, :string, size: 4
    field :mode_s, :string, size: 6
    field :mode_s_country, :string, size: 40
    field :registration, :string, size: 20
    field :source, :string, size: 255
    field :source_type, :string, size: 255, default: "modes"
    field :type_flight, :string, size: 50

    timestamps()
  end

  @doc false
  def changeset(aircraft_mode, attrs) do
    aircraft_mode
    |> cast(attrs, [
      :mode_s,
      :mode_s_country,
      :registration,
      :icao_type_code,
      :type_flight,
      :source,
      :source_type
    ])
    |> validate_required([:mode_s])
    |> unique_constraint(:icao_type_code)
  end
end
