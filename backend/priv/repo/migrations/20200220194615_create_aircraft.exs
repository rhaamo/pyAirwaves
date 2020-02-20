defmodule Pyairwaves.Repo.Migrations.CreateAircraft do
  use Ecto.Migration

  def change do
    create_if_not_exists table(:aircraft) do
      add :aircraft_description, :string, default: nil, size: 255
      add :aircraft_shadow, :string, default: nil, size: 255
      add :engine_count, :integer, default: nil
      add :engine_type, :string, default: nil
      add :icao, :string, size: 10
      add :manufacturer, :string, size: 255
      add :mfr, :string, default: nil
      add :official_page, :string, size: 255
      add :type, :string, size: 255
      add :wake_category, :string, size: 10
    end

  end
end
