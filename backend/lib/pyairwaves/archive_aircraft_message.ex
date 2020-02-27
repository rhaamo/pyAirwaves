defmodule Pyairwaves.ArchiveAircraftMessage do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_aircraft_message" do
    # Specific to source
    # SBS, RAW MODE-S, ...
    field :source_type, :string

    # Specific to SBS
    field :hex_ident, :string
    field :msg_type, :string
    field :transmission_type, :integer
    field :session_id, :string
    field :aircraft_id, :string
    field :flight_id, :string
    field :generated, :naive_datetime
    field :callsign, :string, default: "@@@@@@@@"
    field :altitude, :integer
    field :ground_speed, :integer
    field :track, :integer
    field :geom, Geo.PostGIS.Geometry
    field :vertical_rate, :integer
    field :squawk, :string
    field :alert, :boolean
    field :emergency, :boolean
    field :spi_ident, :boolean
    field :is_on_ground, :boolean

    belongs_to :archive_aircraft, Pyairwaves.ArchiveAircraft
    belongs_to :archive_source, Pyairwaves.ArchiveSource

    # AKA "logged" in SBS
    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [
      :source_type,
      :hex_ident,
      :msg_type,
      :transmission_type,
      :session_id,
      :aircraft_id,
      :flight_id,
      :generated,
      :callsign,
      :altitude,
      :ground_speed,
      :track,
      :geom,
      :vertical_rate,
      :squawk,
      :alert,
      :emergency,
      :spi_ident,
      :is_on_ground
    ])
    |> validate_required([:source_type, :hex_ident])
    |> validate_number(:transmission_type, greater_than_or_equal_to: 1, less_than_or_equal_to: 8)
    |> validate_inclusion(:msg_type, ["MSG", "STA", "ID", "AIR", "SEL", "CLK"])
    |> validate_length(:callsign, max: 8)
  end
end
