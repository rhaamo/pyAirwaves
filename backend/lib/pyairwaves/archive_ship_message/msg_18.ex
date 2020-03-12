defmodule Pyairwaves.ArchiveShipMessage.Msg18 do
  use Ecto.Schema

  # AIS Standard Class B Equipment Position Report
  embedded_schema do
    field :channel, :string
    field :checksum, :string
    field :class_b_band_flag, :integer
    field :class_b_display_flag, :integer
    field :class_b_dsc_flag, :integer
    field :class_b_message_22_flag, :integer
    field :class_b_unit_flag, :integer
    field :cog, :float
    field :communication_state, :integer
    field :communication_state_selector_flag, :integer
    field :current, :string
    field :formatter, :string
    field :latitude, :float
    field :longitude, :float
    field :message_id, :integer
    field :mode_flag, :integer
    field :padding, :string
    field :payload, :string
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :repeat_indicator, :integer
    field :sequential, :string
    field :sog, :float
    field :spare1, :integer
    field :spare2, :integer
    field :talker, :string
    field :time_stamp, :integer
    field :total, :string
    field :true_heading, :integer
    field :user_id, :integer
  end
end
