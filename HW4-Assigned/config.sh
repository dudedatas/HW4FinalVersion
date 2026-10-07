
PROJECT_ID="dsai692-data-acquisition"


REGION="us-central1"


ENV_FILE="/Users/mike/woodbridge/dsai692_data_acquisition_2026/HW3-Assigned/HW2-Assigned/.env"


LOCAL_KEY_FILE="/Users/mike/.ssh/dsai692-data-acquisition-key.json"


API_PORT="8000"
WEBAPP_PORT="8501"

# ---------------------------------------------------------------------
# Provided -- no need to change anything below this line.
# ---------------------------------------------------------------------

# Secret Manager holds the key, and we need to mount it.
GCP_KEY_SECRET=hw3-gcp-key
SECRET_MOUNT_PATH=/run/secrets/gcp_key

# Cloud Run service names.
API_SERVICE=hw3-api-server
WEBAPP_SERVICE=hw3-webapp

# Cloud Scheduler job: name, schedule, and the request body.
SCHEDULER_JOB=hw3-refresh-jobs-trigger
SCHEDULE="0 0 * * *"
MESSAGE_BODY='{"job_title":"Data Engineer", "company_dict":{"Google":"www.google.com/about/careers/applications/jobs","OpenAI":"openai.com/careers","Anthropic":"anthropic.com/careers/jobs"}}'

# The API endpoint, and the GCS prefix.
SEARCH_PATH=/search_and_save/jobs
FILE_NAME_PREFIX=job_search

# =====================================================================
# Validation 
# =====================================================================
for _hw3_var in PROJECT_ID REGION ENV_FILE LOCAL_KEY_FILE API_PORT \
                WEBAPP_PORT; do
  if [ -z "${!_hw3_var}" ]; then
    echo "ERROR: $_hw3_var is empty - fill in TODOs in config.sh" \
         "before running this script." >&2
    exit 1
  fi
done
unset _hw3_var

if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: ENV_FILE '$ENV_FILE' does not exist." >&2
  exit 1
fi
if [ ! -f "$LOCAL_KEY_FILE" ]; then
  echo "ERROR: LOCAL_KEY_FILE '$LOCAL_KEY_FILE' does not exist." >&2
  exit 1
fi
