defmodule Pyairwaves.ArchiveShipMessage.Msg14 do
  use Ecto.Schema

  # AIS Safety Related Broadcast Message
  embedded_schema do
    field :channel, :string
    field :checksum, :string
    field :current, :string
    field :formatter, :string
    field :message_id, :integer
    field :padding, :string
    field :payload, :string
    field :repeat_indicator, :integer
    field :safety_related_text, :string
    field :sequential, :string
    field :source_id, :integer
    field :spare, :integer
    field :talker, :string
    field :total, :string
  end
end
