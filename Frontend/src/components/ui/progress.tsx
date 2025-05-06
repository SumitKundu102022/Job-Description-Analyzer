import React, { forwardRef } from "react";
import { ProgressBar } from "react-bootstrap";
import { cn } from "../../lib/utils";

export interface ProgressProps
  extends React.ComponentPropsWithoutRef<typeof ProgressBar> {
  className?: string;
  value?: number;
  color?: string; // Add color prop
  variant?:
    | "primary"
    | "secondary"
    | "success"
    | "danger"
    | "warning"
    | "info"
    | "light"
    | "dark";
}

const Progress = forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, color, variant = "primary", ...props }, ref) => {
    const style = {
      ...props.style,
      backgroundColor: color, // Apply color
    };

    return (
      <ProgressBar
        ref={ref}
        now={value}
        variant={variant}
        className={cn("w-full", className)}
        style={style}
        {...props}
      />
    );
  }
);
Progress.displayName = "Progress";

export { Progress };
