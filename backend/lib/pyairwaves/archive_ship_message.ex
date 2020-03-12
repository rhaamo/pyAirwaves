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

    # New fields
    # Class A AIS Position Report
    embeds_one(:msg_123, Pyairwaves.ArchiveShipMessage.Msg123)
    # AIS Base Station Report
    embeds_one(:msg_4, Pyairwaves.ArchiveShipMessage.Msg4)
    # AIS Class A Ship Static And Voyage Related Data
    embeds_one(:msg_5, Pyairwaves.ArchiveShipMessage.Msg5)
    # AIS Standard Search And Rescue Aircraft Position Report
    embeds_one(:msg_9, Pyairwaves.ArchiveShipMessage.Msg9)
    # AIS Addressed Safety Related Message
    embeds_one(:msg_12, Pyairwaves.ArchiveShipMessage.Msg12)
    # AIS Safety Related Broadcast Message
    embeds_one(:msg_14, Pyairwaves.ArchiveShipMessage.Msg14)
    # AIS Standard Class B Equipment Position Report
    embeds_one(:msg_18, Pyairwaves.ArchiveShipMessage.Msg18)
    # AIS Aids To Navigation (ATON) ReportAIS Aids To Navigation (ATON) Report
    embeds_one(:msg_21, Pyairwaves.ArchiveShipMessage.Msg21)

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
      :eta,
      :msg_123
    ])
    |> validate_required([:mmsi, :raw])
  end
end
