defmodule Pyairwaves.Repo.Migrations.AddSourceEntrypointDataorigin do
  use Ecto.Migration

  def change do
    alter table("archive_source") do
      add :entrypoint, :string
      add :data_origin, :string
    end
  end
end
