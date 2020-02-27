defmodule Pyairwaves.ArchiveShipMessage do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_ship_message" do
    field :mmsi, :integer
    field :raw, :string
    field :assembled, :boolean, default: false
    field :geom, Geo.PostGIS.Geometry
    field :heading, :float
    field :course_over_ground, :float
    field :turn_rate, :float
    field :position_accuracy, :boolean, default: false
    field :maneuver, :integer
    field :raim, :boolean, default: true
    field :radio_status, :integer
    field :destination, :string
    field :callsign, :string
    field :epfd, :string
    field :navigation_status, :string
    field :draught, :float
    field :eta, :string

    belongs_to :archive_ship, Pyairwaves.ArchiveShip
    belongs_to :archive_source, Pyairwaves.ArchiveSource

    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [
      :mmsi,
      :raw,
      :assembled,
      :geom,
      :heading,
      :course_over_ground,
      :turn_rate,
      :position_accuracy,
      :maneuver,
      :raim,
      :radio_status,
      :destination,
      :callsign,
      :epfd,
      :navigation_status,
      :draught,
      :eta
    ])
    |> validate_required([:mmsi, :raw])
  end
end
