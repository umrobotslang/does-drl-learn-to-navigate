local random = require 'common.random'
local factory = require 'factories.text_random_spawn_factory'

-- Requirements for entityLayer while makeMap
-- (Handled by entityLayer:gsub("[GAP ]", "P", 1):gsub("[GAP ]", "A"))
-- 1. Atleast one "P"
-- 2. All probable locations should be have A
--
-- Requirements for entityLayer while using it to generate randomGoals
-- 1. Place G where you want the possible goal locations to be
-- 2. The robot will spawn at some random location at distance > 8 from chosen G
-- 3. Apples will be replace with Apple at scatteredRewardDensity probability
local entityLayer_01 = [[
{{maze_entity}}
]]


local entityLayer = entityLayer_01
local variationsLayer = variationsLayer_01

local mapName = '{{mapname}}'
local numMaps = {{numMaps}}
local chosenMap = random.uniformInt(0, numMaps-1)
local nextMapName = mapName--string.format('random_map_%03d', chosenMap)

local create_new_map = {{makeMap}}
if create_new_map then
    local make_map = require 'common.make_map'
    make_map.makeMap(mapName, 
                     entityLayer)
end

return factory.createLevelApi{
    mapName = mapName
    , blankMapName = '{{mapname}}_blank_name'
    , entityLayer = entityLayer
    , episodeLengthSeconds = {{time}} 
    , scatteredRewardDensity = 0.25
    , minSpawnGoalDistance = 0
    , numMaps = numMaps
    , mapdir = '{{mapdir}}'
}
