module.exports = {
    apps: [
      {
        name: "pura-crew",
        script: "uvicorn",
        args: "api:app --host 0.0.0.0 --port 7778",
        interpreter: "python3",
        watch: true,
        autorestart: true,
      },
    ],
  };
  
