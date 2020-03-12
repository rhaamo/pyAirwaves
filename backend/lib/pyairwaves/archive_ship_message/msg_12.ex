defmodule Pyairwaves.ArchiveShipMessage.Msg12 do
  use Ecto.Schema

  # AIS Addressed Safety Related Message
  embedded_schema do
    field :channel, :string
    field :checksum, :string
    field :current, :string
    field :destination_id, :integer
    field :formatter, :string
    field :message_id, :integer
    field :padding, :string
    field :payload, :string
    field :repeat_indicator, :integer
    field :retransmit_flag, :integer
    field :safety_related_text, :string
    field :sequence_number, :integer
    field :sequential, :string
    field :source_id, :integer
    field :spare, :integer
    field :talker, :string
    field :total, :string
  end
end
