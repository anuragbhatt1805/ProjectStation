from django.db import models
from django.conf import settings

# Create your models here.
class PushRecord(models.Model):
    record = models.ForeignKey('TaskRecord', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=False, choices=[
        ('START', 'Start'),
        ('END', 'End'),
        ('RESUME', 'Resume'),
        ('SUSPEND', 'Suspend'),
    ], verbose_name='Record Type')
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class TaskRecord(models.Model):
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, verbose_name='Task')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Employee')

    class Meta:
        unique_together = ('task', 'user')

    objects = models.Manager()

    def add_start_punch(self):
        punch = PushRecord.objects.create(record=self, type='START')
        self.task.status = 'IN-PROGRESS'
        self.task.save()
        punch.save()
        return punch
    
    def add_end_punch(self):
        punch = PushRecord.objects.create(record=self, type='END')
        self.task.status = 'IN-REVIEW'
        self.task.save()
        punch.save()
        return punch
    
    def add_resume_punch(self):
        punch = PushRecord.objects.create(record=self, type='RESUME')
        self.task.status = 'IN-PROGRESS'
        self.task.save()
        punch.save()
        return punch
    
    def add_suspend_record(self):
        punch = PushRecord.objects.create(record=self, type='SUSPEND')
        self.task.status = 'BREAK'
        self.task.save()
        punch.save()
        return punch
    
    def get_punches(self):
        return PushRecord.objects.filter(record=self).order_by('timestamp')
    
    def get_total_time(self):
        punches = self.get_punches()
        if len(punches) == 0:
            return 0
        else:
            start_time = None
            end_time = None
            total_time = 0

            for punch in punches:
                if punch.type == 'START':
                    start_time = punch.timestamp
                elif punch.type == 'END':
                    end_time = punch.timestamp
                elif punch.type == 'SUSPEND':
                    end_time = punch.timestamp
                    if start_time and end_time:
                        total_time += (end_time - start_time).total_seconds()
                    start_time = None
                    end_time = None
                elif punch.type == 'RESUME':
                    start_time = punch.timestamp

            if start_time and end_time:
                total_time += (end_time - start_time).total_seconds()

            return total_time