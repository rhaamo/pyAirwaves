defmodule Pyairwaves.Repo.Migrations.AddAircraftArchiving do
  use Ecto.Migration

  def change do
    create_if_not_exists table("archive_aircraft") do
      add :hex_ident, :string

      timestamps()
    end

    create_if_not_exists table("archive_aircraft_message") do
      add :source_type, :string

      add :hex_ident, :string
      add :msg_type, :string
      add :transmission_type, :integer
      add :session_id, :string
      add :aircraft_id, :string
      add :flight_id, :string
      add :generated, :naive_datetime
      add :callsign, :string, default: "@@@@@@@@"
      add :altitude, :integer
      add :ground_speed, :integer
      add :track, :integer
      add :geom, :geometry
      add :vertical_rate, :integer
      add :squawk, :string
      add :alert, :boolean
      add :emergency, :boolean
      add :spi_ident, :boolean
      add :is_on_ground, :boolean

      add :archive_aircraft_id, references(:archive_aircraft)
      add :archive_source_id, references(:archive_source)

      timestamps()
    end
  end
end
