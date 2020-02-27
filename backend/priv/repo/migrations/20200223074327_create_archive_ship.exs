defmodule Pyairwaves.Repo.Migrations.CreateArchiveShip do
  use Ecto.Migration

  def change do
    create_if_not_exists table("archive_ship") do
      add :mmsi, :integer
      add :mmsi_type, :string
      add :mmsi_cc, :string
      add :callsign, :string
      add :dim_to_bow, :integer
      add :dim_to_stern, :integer
      add :dim_to_port, :integer
      add :dim_to_starboard, :integer
      add :ship_type, :string

      # has_many :archive_ship_messages

      timestamps()
    end
  end
end
