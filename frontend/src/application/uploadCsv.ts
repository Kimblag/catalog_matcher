import type { ApiError } from '../types';

type UploadCsvParams<T> = {
  file: File;
  service: {
    uploadCsv(
      file: File,
      signal: AbortSignal,
    ): Promise<{ data?: T; error?: ApiError }>;
  };
  signal: AbortSignal;
};

export async function uploadCsv<T>({
  file,
  service,
  signal,
}: UploadCsvParams<T>) {
  return service.uploadCsv(file, signal);
}
