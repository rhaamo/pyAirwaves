defmodule Pyairwaves.ArchiveShipMessage do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_ship_message" do
    field :mmsi, :integer
    field :raw, :string
    field :assembled, :boolean
    field :geom, Geo.PostGIS.Geometry
    field :heading, :float
    field :course_over_ground, :float
    field :turn_rate, :float
    field :position_accuracy, :boolean
    field :maneuver, :integer
    field :raim, :boolean
    field :radio_status, :integer
    field :destination, :string
    field :callsign, :string
    field :epfd, :string
    field :navigation_status, :string
    field :draught, :float
    field :eta, :string

    belongs_to :archive_ship, Pyairwaves.ArchiveShip
    belongs_to :source, Pyairwaves.ArchiveSource

    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [
      :mmsi,
      :mmsi_type,
      :mmsi_cc,
      :callsign,
      :dim_to_bow,
      :dim_to_stern,
      :dim_to_port,
      :dim_to_starboard,
      :ship_type
    ])
    |> validate_required([:mmsi, :mmsi_type, :mmsi_cc])
    |> unique_constraint(:mmsi)
    |> unique_constraint(:callsign)
  end
end
