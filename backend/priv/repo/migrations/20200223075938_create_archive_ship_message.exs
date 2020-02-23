defmodule Pyairwaves.Repo.Migrations.CreateArchiveShipMessage do
  use Ecto.Migration

  def change do
    create_if_not_exists table("archive_ship_message") do
      add :mmsi, :integer
      add :raw, :string
      add :assembled, :boolean, default: false
      add :geom, :geometry
      add :heading, :float
      add :course_over_ground, :float
      add :turn_rate, :float
      add :position_accuracy, :boolean, default: false
      add :maneuver, :integer
      add :raim, :boolean, default: true
      add :radio_status, :integer
      add :destination, :string
      add :callsign, :string
      add :epfd, :string
      add :navigation_status, :string
      add :draught, :float
      add :eta, :string

      add :archive_ship_id, references(:archive_ship)
      add :archive_source_id, references(:archive_source)

      timestamps()
    end
  end
end
