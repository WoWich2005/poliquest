from rest_framework import serializers

from main.models import Stat


class StatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['point', 'team', 'type']

    def validate(self, data):
        arrival_stats = Stat.objects.filter(
            team=data['team'],
            point=data['point'],
            type=Stat.ARRIVAL_TYPE
        )

        start_quest_stats = Stat.objects.filter(
            team=data['team'],
            point=data['point'],
            type=Stat.START_QUEST_TYPE
        )

        finish_quest_stats = Stat.objects.filter(
            team=data['team'],
            point=data['point'],
            type=Stat.FINISH_QUEST_TYPE
        )

        if data['type'] == Stat.ARRIVAL_TYPE:
            team_stats = list(Stat.objects.filter(
                team=data['team']
            ).order_by('time'))[-1:]

            if len(team_stats) != 0:
                if team_stats[0].type != Stat.FINISH_QUEST_TYPE:
                    raise serializers.ValidationError("Команда должна завершить квест на предыдущей точке")

            if len(arrival_stats) != 0:
                raise serializers.ValidationError("Команда уже прибывала на эту точку")
        elif data['type'] == Stat.START_QUEST_TYPE:
            if len(arrival_stats) != 1:
                raise serializers.ValidationError("Команда сначала должна прибыть на эту точку")

            if len(start_quest_stats) != 0:
                raise serializers.ValidationError("Команда уже начинала квест на этой точке")
        elif data['type'] == Stat.FINISH_QUEST_TYPE:
            if len(arrival_stats) != 1:
                raise serializers.ValidationError("Команда сначала должна прибыть на эту точку")

            if len(start_quest_stats) != 1:
                raise serializers.ValidationError("Команда сначала должна начать квест на этой точке")

            if len(finish_quest_stats) != 0:
                raise serializers.ValidationError("Команда уже завершала квест на этой точке")
        else:
            raise serializers.ValidationError("Неизвестный тип действия")

        return data


class StatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['time']
