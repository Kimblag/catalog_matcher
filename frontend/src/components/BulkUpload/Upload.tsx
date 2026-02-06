import type { UploadProps } from '../../types/Upload.types';

const Upload = ({ onFileChange }: UploadProps) => {
  return (
    <form>
      <input
        onChange={(e) => onFileChange(e)}
        type="file"
        id="file-upload"
        name="upload-file"
      />
    </form>
  );
};

export default Upload;
