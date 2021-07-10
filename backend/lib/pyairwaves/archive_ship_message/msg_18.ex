defmodule Pyairwaves.ArchiveShipMessage.Msg18 do
  use Ecto.Schema

  # AIS Standard Class B Equipment Position Report
  embedded_schema do
    # AIS
    field :class_b_band_flag, :integer
    field :class_b_display_flag, :integer
    field :class_b_dsc_flag, :integer
    field :class_b_message_22_flag, :integer
    field :class_b_unit_flag, :integer
    field :cog, :float
    field :communication_state, :integer
    field :communication_state_selector_flag, :integer
    field :latitude, :float
    field :longitude, :float
    field :mode_flag, :integer
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :repeat_indicator, :integer
    field :sog, :float
    field :spare1, :integer
    field :spare2, :integer
    field :time_stamp, :integer
    field :true_heading, :integer
    field :user_id, :integer

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
