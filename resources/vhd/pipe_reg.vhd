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
entity pipe_reg is
  generic(data_width : natural);
  port ( 
    clock    : in  std_logic;
    reset_n  : in  std_logic;
    enable   : in  std_logic;
    data_in  : in  std_logic_vector (data_width-1 downto 0);
    data_out : out std_logic_vector (data_width-1 downto 0));
end pipe_reg;
architecture behavioral of pipe_reg is
  signal tmp : std_logic_vector(data_width-1 downto 0) := (others => '0');
begin
  data_out <= tmp;
  process(clock, reset_n, data_in, enable)
    begin
      if reset_n = '0' then
        tmp <= (others => '0');
      elsif enable = '1' and rising_edge(clock) then
        tmp <= data_in;
      end if;
    end process;
end behavioral;
