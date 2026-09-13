<script setup lang="ts">
import { CircleCheck, CircleX, LoaderCircle, ShieldBan } from 'lucide-vue-next';
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';

type ServiceConnectionState =
  'checking' | 'reachable' | 'denied' | 'unavailable';
interface ActiveRequest {
  controller: AbortController;
  timeoutId: number;
}

const connectionState = ref<ServiceConnectionState>('checking');
let activeRequest: ActiveRequest | undefined;

const connectionLabel = computed(() => {
  if (connectionState.value === 'reachable') {
    return '服務可連線';
  }

  if (connectionState.value === 'unavailable') {
    return '服務無法連線';
  }

  if (connectionState.value === 'denied') {
    return '存取遭拒';
  }

  return '檢查中';
});

const shouldOfferRetry = computed(
  () =>
    connectionState.value === 'denied' ||
    connectionState.value === 'unavailable'
);

function cancelActiveRequest(): void {
  if (activeRequest === undefined) {
    return;
  }

  window.clearTimeout(activeRequest.timeoutId);
  activeRequest.controller.abort();
  activeRequest = undefined;
}

async function checkServiceConnection(): Promise<void> {
  cancelActiveRequest();
  connectionState.value = 'checking';
  const controller = new AbortController();
  const request: ActiveRequest = {
    controller,
    timeoutId: window.setTimeout(() => {
      controller.abort();
    }, 5_000)
  };
  activeRequest = request;

  try {
    const response = await fetch('/health', {
      cache: 'no-store',
      signal: controller.signal
    });

    if (activeRequest !== request) {
      return;
    }

    if (response.status === 403) {
      connectionState.value = 'denied';
      return;
    }

    if (response.status !== 200) {
      connectionState.value = 'unavailable';
      return;
    }

    const payload: unknown = await response.json();

    if (activeRequest !== request) {
      return;
    }

    connectionState.value =
      typeof payload === 'object' &&
      payload !== null &&
      'status' in payload &&
      payload.status === 'ok'
        ? 'reachable'
        : 'unavailable';
  } catch {
    if (activeRequest === request) {
      connectionState.value = 'unavailable';
    }
  } finally {
    if (activeRequest === request) {
      window.clearTimeout(request.timeoutId);
      activeRequest = undefined;
    }
  }
}

onMounted(() => {
  void checkServiceConnection();
});

onBeforeUnmount(() => {
  cancelActiveRequest();
});
</script>

<template>
  <section
    class="settings-section"
    aria-labelledby="service-connection-heading"
  >
    <h2 id="service-connection-heading">服務連線</h2>

    <div
      class="service-connection-row"
      :class="`service-connection-row--${connectionState}`"
      aria-live="polite"
    >
      <LoaderCircle
        v-if="connectionState === 'checking'"
        class="checking-icon"
        aria-hidden="true"
        :size="20"
      />
      <CircleCheck
        v-else-if="connectionState === 'reachable'"
        aria-hidden="true"
        :size="20"
      />
      <ShieldBan
        v-else-if="connectionState === 'denied'"
        aria-hidden="true"
        :size="20"
      />
      <CircleX v-else aria-hidden="true" :size="20" />
      <span>{{ connectionLabel }}</span>
      <button
        v-if="shouldOfferRetry"
        type="button"
        @click="checkServiceConnection"
      >
        重新檢查
      </button>
    </div>
  </section>
</template>

<style scoped>
.settings-section {
  margin-top: 24px;
  padding: 20px 0;
  border-top: 1px solid var(--border-default);
  border-bottom: 1px solid var(--border-default);
}

h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
}

.service-connection-row {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 48px;
  margin-top: 20px;
  padding: 8px 12px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-control);
  background: var(--bg-surface);
  color: var(--text-secondary);
}

.service-connection-row--reachable {
  border-color: var(--status-success-border);
  background: var(--status-success-background);
  color: var(--status-success-foreground);
}

.service-connection-row--denied {
  border-color: var(--status-warning-border);
  background: var(--status-warning-background);
  color: var(--status-warning-foreground);
}

.service-connection-row--unavailable {
  border-color: var(--status-danger-border);
  background: var(--status-danger-background);
  color: var(--status-danger-foreground);
}

.checking-icon {
  animation: spin 900ms linear infinite;
}

.service-connection-row button {
  min-height: 44px;
  margin-left: auto;
  padding: 0 12px;
  border: 1px solid currentcolor;
  border-radius: var(--radius-control);
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.service-connection-row button:hover {
  background: var(--bg-hover);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
