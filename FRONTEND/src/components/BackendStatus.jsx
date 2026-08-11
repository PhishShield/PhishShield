import { useEffect, useState } from "react";
import { checkBackendHealth } from "./api/healthApi";

function BackendStatus() {
  const [online, setOnline] = useState(false);

  useEffect(() => {
    const checkStatus = async () => {
      const result = await checkBackendHealth();
      setOnline(result);
    };

    checkStatus();

    const interval = setInterval(checkStatus, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {online ? (
        <span>🟢 Backend Online</span>
      ) : (
        <span>🔴 Backend Offline</span>
      )}
    </div>
  );
}

export default BackendStatus;