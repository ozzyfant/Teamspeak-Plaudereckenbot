#!/usr/bin/python
import plaudereckenbot
import time
import yaml

with open("config.yml", 'r') as configfile:
    cfg = yaml.load(configfile)


pBot = plaudereckenbot.pBot(cfg['server_host'],
                            cfg['query_port'],
                            cfg['query_user'],
                            cfg['query_password'],
                            cfg['displayname'],
                            cfg['virtual_server_sid'],
                            cfg['fixed_channels'][:],
                            cfg['parent_channel_id'],
                            cfg['channel_name_template'])
while 1:
    emptyRooms = 0
    pBot.getUserInfo()
    channelUserCount = list()
    print "userInfo: " + str(pBot.userInfoArray)
    for i in range(len(pBot.channellist)):
        channelUserCount.append(pBot.getChannelUsers(pBot.channellist[i]))
    for i in range(len(channelUserCount)):
        if(channelUserCount[i] > 0):
            channelUserCount[i] = True
        else:
            emptyRooms = emptyRooms + 1
    print "ChanUserCount: " + str(channelUserCount)
    print "lenSetUserCount: " + str(len(set(channelUserCount)) == 1
    and channelUserCount[0] == True)
    if len(set(channelUserCount)) == 1 and channelUserCount[0] == True:
        pBot.addChannel()
    print "emptyRooms: " + str(emptyRooms)
    deletedChannels = 0
    if emptyRooms > 1:
        for i in reversed(range(len(pBot.channellist))):
            if channelUserCount[i] == 0 and (deletedChannels + 1) < emptyRooms:
                if pBot.channellist[i] not in cfg['fixed_channels']:
                    pBot.delChannel(pBot.channellist[i])
                    deletedChannels = deletedChannels + 1
            else:
                break
    time.sleep(5)
