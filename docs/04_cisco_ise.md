# Merlin on ISE 

## Enable ERS

![Enable ERS](images/04_step01.png)

![Enable ERS](images/04_step02.png)

ISE RBAC requires ERS permissions be set

![Enable ERS](images/04_step03.png)

![Enable ERS](images/04_step04.png)

## Enable MnT

![Enable ERS](images/04_step05.png)

![Enable ERS](images/04_step06.png)

MnT Permissions

![Enable ERS](images/04_step07.png)

## Update your testbed

```yaml

devices:
    ISE:
      alias: 'ISE'
      type: 'ISE'
      os: 'ISE'
      platform: ISE
      credentials:
        default:
          username: {{ your ISE API username }}
          password: {{ your ISE API password }}
      connections:
          ip: "{{ your ISE IP }}"
```

### Run Merlin on ISE 

```console
pyats run job ISE_merlin_job.py
```

```bash
cd Camelot

ls 
```

To view the pyATS log in a web browser Locally

```bash
pyats logs view
```

To view the pyATS log in a web browser remotely

```bash
pyats logs view --host 0.0.0.0 --port 8080 -v
```

![Sample Log](images/pyATS_Log_Viewer.png)

[Back to the main project](https://github.com/automateyournetwork/merlin)