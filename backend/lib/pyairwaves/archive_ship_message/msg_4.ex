defmodule Pyairwaves.ArchiveShipMessage.Msg4 do
  use Ecto.Schema

  # AIS Base Station Report
  embedded_schema do
    # AIS
    field :communication_state, :integer
    field :latitude, :float
    field :longitude, :float
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :repeat_indicator, :integer
    field :spare, :integer
    field :transmission_control_for_long_range_broadcast_message, :integer
    field :type_of_electronic_position_fixing_device, :integer
    field :user_id, :integer
    field :utc_day, :integer
    field :utc_hour, :integer
    field :utc_minute, :integer
    field :utc_second, :integer
    field :utc_year, :integer
    # TODO: DateTime naive in utc
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
