# Attendance Cog

A cog to take the attendance (Roll Call) of a particular voice channel and output it to a text channel

## Commands

```
[p]attendance or [p]attend
[p]attendance_channel or [p]attendchan
```

## Help
- **attend** - Takes the attendance from a specified voice channel.\n
Syntax: '[p]attend <voice> [role] [channel] [per_page]'
  -	***\<voice\>*** - Specify the voice channel, in quotes, that you would like to take attendance of.
  -	***[role]*** - *Optional* - Limits the attendance to only those people in the specified role.
  - ***[channel]*** - *Optional* - Outputs attendance to a specific channel, if not specified then the default channel is used.
  -	***[per_page]*** - *Optional* - Specifies the amount of people to list per page in a dynamic list with pagination. Specify 0 here to create a list of all attendees that will not be paginated and can be reviewed later

2. **attendchan** - sets the default text-channel to be used for output, if no channel is specified in the syntax.

## Known Issues
Due to the paging option, if you have a voice channel where the name is just a number, the cog cannot distinguish between a paging request and the channel name, so it will not report attendance from such channels.

## WolfLAN
WolfLAN Gaming Community - http://wolflan.com