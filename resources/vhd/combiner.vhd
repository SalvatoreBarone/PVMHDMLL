-- Copyright 2020-2021 Salvatore Barone <salvatore.barone@unina.it>
-- 
-- This file is part of PVMHDMLL
-- 
-- This is free software; you can redistribute it and/or modify it under
-- the terms of the GNU General Public License as published by the Free
-- Software Foundation; either version 3 of the License, or any later version.
-- 
-- This is distributed in the hope that it will be useful, but WITHOUT
-- ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
-- FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
-- more details.
-- 
-- You should have received a copy of the GNU General Public License along with
-- RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
-- Street, Fifth Floor, Boston, MA 02110-1301, USA.

library ieee;
use ieee.std_logic_1164.all;
entity swapper_cell is
	port (
		data_in  : in std_logic_vector(1 downto 0);
		data_out : out std_logic_vector(1 downto 0));
end entity;
architecture swapper_cell of swapper_cell is
begin
	data_out(0) <= data_in(0) and data_in(1);
	data_out(1) <= data_in(0) or data_in(1);
end architecture;


library ieee;
use ieee.std_logic_1164.all;
entity swapper_block is
	generic (data_width : natural);
	port (
		data_in  : in std_logic_vector(data_width-1 downto 0);
		data_out : out std_logic_vector(data_width-1 downto 0));
end entity;
architecture dataflow of swapper_block is
	component swapper_cell is
    port (
      data_in  : in std_logic_vector(1 downto 0);
      data_out : out std_logic_vector(1 downto 0));
  end component;
	signal intermediate_data : std_logic_vector(data_width-1 downto 0) := (others => '0');
begin
	first_stage_swappers : for i in data_width/2-1 downto 0 generate
		fst_stg_cell : swapper_cell port map (data_in(2*i+1 downto 2*i), intermediate_data(2*i+1 downto 2*i));
	end generate;
	second_stage_swappers : for i in data_width/2-1 downto 1 generate
    snd_stg_cell : swapper_cell	port map (intermediate_data(2*i downto 2*i-1), data_out(2*i downto 2*i-1));
  end generate;
	data_out(0) <= intermediate_data(0);
	data_out(data_width-1) <= intermediate_data(data_width-1);
end dataflow;


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
entity combiner is
	generic	(
		data_width  : natural;
		pipe_stages : natural);
  port (
    clock    : in  std_logic;
		reset_n  : in  std_logic;
		data_in  : in  std_logic_vector (data_width-1 downto 0);
   	majority : out std_logic);
end combiner;
architecture combiner of combiner is
	component swapper_block is
    generic (data_width : natural);
    port (
      data_in  : in std_logic_vector(data_width-1 downto 0);
      data_out : out std_logic_vector(data_width-1 downto 0));
  end component;
  component pipe_reg is
    generic(data_width : natural);
    port ( 
      clock    : in  std_logic;
      reset_n  : in  std_logic;
      enable   : in  std_logic;
      data_in  : in  std_logic_vector (data_width-1 downto 0);
      data_out : out std_logic_vector (data_width-1 downto 0));
  end component;
	constant swapper_per_pipe : natural := data_width / pipe_stages;
	type matrix is array (natural range <>) of std_logic_vector (data_width-1 downto 0);
	signal intermediates : matrix (0 to data_width + pipe_stages);
begin
	assert pipe_stages mod 2 = 0	report "pipe_stages must be a power of two"	severity failure;
	data_in_buffer : pipe_reg	generic map (data_width)	port map (clock, reset_n, '1', data_in, intermediates(0));
	majority <=	intermediates(data_width + pipe_stages)(data_width/2);
	chain : for i in 0 to data_width + pipe_stages - 1 generate
    pipe : if (i+1) mod (swapper_per_pipe+1) = 0 generate 
      pipe_buffer: pipe_reg	generic map (data_width) port map (clock, reset_n, '1', intermediates(i), intermediates(i+1));
    end generate;
    swapper : if (i+1) mod (swapper_per_pipe+1) /= 0 generate 
      swapper_inst: swapper_block generic map (data_width) port map(intermediates(i), intermediates(i+1));
    end generate;
	end generate;
end architecture;
