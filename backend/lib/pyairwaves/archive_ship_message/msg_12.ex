defmodule Pyairwaves.ArchiveShipMessage.Msg12 do
  use Ecto.Schema

  # AIS Addressed Safety Related Message
  embedded_schema do
    # AIS
    field :destination_id, :integer
    field :repeat_indicator, :integer
    field :retransmit_flag, :integer
    field :safety_related_text, :string
    field :sequence_number, :integer
    field :source_id, :integer
    field :spare, :integer

    # NMEA
    field :channel, :string
    field :checksum, :string
    field :current, :string
    field :formatter, :string
    field :message_id, :integer
    field :padding, :string
    field :payload, :string
    field :talker, :string
    field :total, :string
    field :sequential, :string
  end
end
